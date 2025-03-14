import maya.api.OpenMaya as OpenMaya

# get matrices
# if 0 differs from the default matrix, notify user and break
# else extract matrix from 1 and inverse
# set 0 matrix to inversed matrix

def get_matrix(object):
    # Create a selection list and add an object to it
    selection_list = OpenMaya.MSelectionList()
    selection_list.add(object)  # Add 'pCube1' to the selection list
    print(selection_list)

    # Retrieve the DAG path of the first object in the selection list
    dagPath = selection_list.getDagPath(0)

    # Get the world matrix of the object
    world_matrix = dagPath.inclusiveMatrix()

    selection_list.clear()
    return world_matrix

def matrix_is_default(matrix: OpenMaya.MMatrix):
    default_matrix = OpenMaya.MMatrix((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
    if matrix == default_matrix:
        return 0

def overcompensate(object: str, dummy: str):
    object = get_matrix(object)
    dummy = get_matrix(dummy)

# objects to transform
list = ["ShadowGeo", "CAM:DUMMY"]
matrix_list = []
for l in list:
    print(l)
    matrix_list.append(get_matrix(l))

print(matrix_list)
inverse_matrix = OpenMaya.MMatrix(matrix_list[1]).inverse()
print(inverse_matrix)

target = matrix_list[0] * inverse_matrix

print(target)

# get object and set matrix to inverse matrix
selection_list = OpenMaya.MSelectionList()
selection_list.add("ShadowGeo")  # Add 'pCube1' to the selection list
print(selection_list)

# Retrieve the DAG path of the first object in the selection list
dagPath_Cube = selection_list.getDagPath(0)
shadow_geo = OpenMaya.MFnTransform(dagPath_Cube)
print(shadow_geo)
inverse_matrix = OpenMaya.MTransformationMatrix(inverse_matrix)
print(inverse_matrix)
shadow_geo.setTransformation(inverse_matrix)
print(shadow_geo.transformation)