import arcgis
from arcgis.gis import GIS

# Deep Learning parameters
_modelPath = "https://edemo7.esri.nl/server/rest/content/items/b5ca03a1f6534365a2fb5157831ae19c"
_inputRaster = "https://tiles.arcgis.com/tiles/emS4w7iyWEQiulAb/arcgis/rest/services/LuchtfotoRotterdam2018/MapServer"
_outputFC = "https://services.arcgis.com/emS4w7iyWEQiulAb/arcgis/rest/services/DetectedObjects_Zebracrossings/FeatureServer/0"
_dlProfileName = "DL_profile"

# Workforce parameters
_pointFCName = "Centroids_for_DetectedObjects_Zebracrossings"
_workforceProjectId = "1e1cff345df64340ba7461a10c6cfead"
_onlineProfileName = "Online_profile"

def deepLearning():
    """Apply a deep learning model on an input raster"""

    # Connect to portal
    portal = GIS("https://edemo7.esri.nl/portal", profile=_dlProfileName)

    # Initialize Model object
    print("Loading model")
    model = arcgis.learn.Model()
    model.from_model_path(_modelPath)
    model.install(gis=portal)

    # Apply model on imagery
    print("Applying model on imagery")
    outputFeatureLayer = arcgis.features.FeatureLayer(_outputFC)
    arcgis.learn.detect_objects(_inputRaster, model, gis=portal, output_name=outputFeatureLayer)

    # Turn detected objects layer into point layer for Workforce
    arcgis.features.analysis.find_centroids(outputFeatureLayer, output_name=_pointFCName)

def main():
    """Add the detected objects to Workforce as new assignments"""

    # Connect to ArcGIS Online
    gis = GIS("https://maps.arcgis.com", profile=_onlineProfileName)

    # Create Workforce items using detected objects
    item = gis.content.get(_workforceProjectId)
    project = arcgis.apps.workforce.Project(item)
    print("Adding detected features to Workforce project: {}".format(project.title))

    # Extra information for assignments
    assignmentType = arcgis.apps.workforce.managers.AssignmentTypeManager(project).search()[0]
    dispatcher = arcgis.apps.workforce.managers.DispatcherManager(project).search()[0]
    worker = arcgis.apps.workforce.managers.WorkerManager(project).search()[0]

    # Create empty list for batch adding of assignments
    assignments = []

    # Query Object Detection Feature Class 
    inputFC = "https://services.arcgis.com/emS4w7iyWEQiulAb/arcgis/rest/services/{}/FeatureServer/0".format(_pointFCName)
    outputFeatureLayer = arcgis.features.FeatureLayer(inputFC)
    features = outputFeatureLayer.query().to_dict()

    # Add features from detected objects as new assignment objects
    count = 1
    for feature in features["features"]:
        print("Processing feature {} of {}".format(count, len(features["features"])))
        geometry = feature["geometry"]
        geometry["spatialReference"] = {"wkid":102100}
        assignment = arcgis.apps.workforce.Assignment(project, geometry=geometry, assignment_type=assignmentType, location="Rotterdam", status="assigned", dispatcher=dispatcher, worker=worker)
        
        assignments.append(assignment)
        count += 1

    # Batch add new assignments
    print("Batch adding {} new assignments".format(len(assignments)))
    assignmentManager = arcgis.apps.workforce.managers.AssignmentManager(project)
    assignmentManager.batch_add(assignments)

    print("Script completed")

if __name__ == "__main__":
    main()
