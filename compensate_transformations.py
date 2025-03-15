import maya.api.OpenMaya as OpenMaya

def get_matrix(object: str):
    """
    Retrieves the DAG path and world transformation matrix of a given object.

    Args:
        object (str): The name of the object in the Maya scene.

    Returns:
        tuple: A tuple containing:
            - dagPath (OpenMaya.MDagPath): The DAG path of the object.
            - world_matrix (OpenMaya.MMatrix): The world transformation matrix of the object.
    """
    selection_list = OpenMaya.MSelectionList()
    selection_list.add(object)
    dagPath = selection_list.getDagPath(0)
    world_matrix = dagPath.inclusiveMatrix()
    selection_list.clear()
    return dagPath, world_matrix

def matrix_is_default(matrix: OpenMaya.MMatrix):
    """
    Checks if the given matrix is the default identity matrix.

    Args:
        matrix (OpenMaya.MMatrix): The matrix to check.

    Returns:
        bool: True if the matrix is the identity matrix, otherwise None.
    """
    default_matrix = OpenMaya.MMatrix(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
    if matrix == default_matrix:
        return True

def inverse_object_matrix(object_matrix: OpenMaya.MMatrix, pivot_matrix: OpenMaya.MMatrix):
    """
    Computes the transformation of an object relative to the inverse of a pivot matrix.

    Args:
        object_matrix (OpenMaya.MMatrix): The transformation matrix of the object.
        pivot_matrix (OpenMaya.MMatrix): The transformation matrix of the pivot object.

    Returns:
        OpenMaya.MTransformationMatrix: The transformed object matrix.
    """
    inverse_matrix = pivot_matrix.inverse()
    object_matrix = object_matrix * inverse_matrix
    object_matrix = OpenMaya.MTransformationMatrix(object_matrix)
    return object_matrix

def set_object_matrix(object_path: OpenMaya.MDagPath, object_matrix: OpenMaya.MTransformationMatrix):
    """
    Sets the transformation matrix of an object.

    Args:
        object_path (OpenMaya.MDagPath): The DAG path of the object.
        object_matrix (OpenMaya.MTransformationMatrix): The transformation matrix to apply.

    Returns:
        OpenMaya.MMatrix: The resulting matrix after applying the transformation.
    """
    object_transform = OpenMaya.MFnTransform(object_path)
    final_matrix = object_transform.setTransformation(object_matrix)
    return final_matrix.transformation().asMatrix()


def overcompensate(object_name: str, pivot_name: str):
    """
    Adjusts the transformation of an object to counteract the transformation of a pivot object.

    Args:
        object_name (str): The name of the object to adjust.
        pivot_name (str): The name of the pivot object used for transformation reference.

    Returns:
        int: Returns 0 if the pivot object is at the default position or if the object is not frozen.
    """
    object_path, object_matrix = get_matrix(object_name)
    pivot_path, pivot_matrix = get_matrix(pivot_name)
    if matrix_is_default(pivot_matrix):
        OpenMaya.MGlobal.displayError("pivot is at default position")
        return 0
    if not matrix_is_default(object_matrix):
        OpenMaya.MGlobal.displayError("Please freeze transforms")
        return 0
    object_matrix = inverse_object_matrix(object_matrix=object_matrix, pivot_matrix=pivot_matrix)
    set_object_matrix(object_path=object_path,object_matrix=object_matrix)