'''OpenGL extension SUN.slice_accum

This module customises the behaviour of the 
OpenGL.raw.GL.SUN.slice_accum to provide a more 
Python-friendly API

Overview (from the spec)
	
	
	This extension defines a new accumulation operation which enables the accumulation
	buffer to be used for alpha compositing. This enables higher precision alpha
	blending than what can be accomplished using the blend operation.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/SUN/slice_accum.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.SUN.slice_accum import *
from OpenGL.raw.GL.SUN.slice_accum import _EXTENSION_NAME

def glInitSliceAccumSUN():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION