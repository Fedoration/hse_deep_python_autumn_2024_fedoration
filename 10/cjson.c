#include <Python.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* concatenate_strings(const char *s1, const char *s2) {
    // Объединение двух строк
    char *char_r = malloc(strlen(s1) + strlen(s2) + 1);
    if (!char_r) {
        return NULL;
    }
    strcpy(char_r, s1);
    strcat(char_r, s2);
    return char_r;
}

char* from_int_to_char(int number) {
    char* buffer = malloc(sizeof(char) * 12);
    if (!buffer) {
        return NULL;
    }
    sprintf(buffer, "%d", number);
    return buffer;
}

PyObject* cjson_dumps(PyObject *self, PyObject *args, PyObject *kwargs) {
    PyObject *dict = NULL, *key = NULL, *value = NULL;
    size_t last = 0;

    if (!PyArg_ParseTuple(args, "O", &dict) || !PyDict_Check(dict)) {
        PyErr_SetString(PyExc_TypeError, "Expected a dictionary.");
        return NULL;
    }

    char* result = malloc(2);
    if (!result) {
        PyErr_SetString(PyExc_MemoryError, "Memory allocation failed.");
        return NULL;
    }
    strcpy(result, "{");

    Py_ssize_t pos = 0;
    while (PyDict_Next(dict, &pos, &key, &value)) {
        char* _key = PyUnicode_AsUTF8(key);
        if (!_key) {
            PyErr_SetString(PyExc_TypeError, "Keys must be strings.");
            free(result);
            return NULL;
        }

        char* formatted_key = concatenate_strings(last ? ", \"" : "\"", _key);
        formatted_key = concatenate_strings(formatted_key, "\": ");
        result = concatenate_strings(result, formatted_key);
        free(formatted_key);

        char* _value = NULL;
        if (PyLong_Check(value)) {
            _value = from_int_to_char(PyLong_AsLong(value));
        } else if (PyUnicode_Check(value)) {
            char* str_value = PyUnicode_AsUTF8(value);
            _value = concatenate_strings("\"", str_value);
            _value = concatenate_strings(_value, "\"");
        } else {
            PyErr_SetString(PyExc_TypeError, "Unsupported value type.");
            free(result);
            return NULL;
        }

        if (!_value) {
            free(result);
            PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory for value.");
            return NULL;
        }

        result = concatenate_strings(result, _value);
        free(_value);

        last++;
    }

    result = concatenate_strings(result, "}");
    PyObject* ret = Py_BuildValue("s", result);
    free(result);
    return ret;
}

PyObject* cjson_loads(PyObject *self, PyObject *args, PyObject *kwargs) {
    char* input_string;
    if (!PyArg_ParseTuple(args, "s", &input_string)) {
        PyErr_SetString(PyExc_TypeError, "Parameter must be a string.");
        return NULL;
    }

    size_t len = strlen(input_string);
    if (len < 2 || input_string[0] != '{' || input_string[len - 1] != '}') {
        PyErr_SetString(PyExc_TypeError, "Expected a JSON object.");
        return NULL;
    }

    PyObject* dict = PyDict_New();
    if (!dict) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to create dictionary object.");
        return NULL;
    }

    char* buffer = strdup(input_string + 1);
    if (!buffer) {
        PyErr_SetString(PyExc_MemoryError, "Memory allocation failed.");
        Py_DECREF(dict);
        return NULL;
    }

    buffer[len - 2] = '\0';
    char* token = strtok(buffer, ",");
    while (token) {
        char* colon_pos = strchr(token, ':');
        if (!colon_pos) {
            PyErr_SetString(PyExc_TypeError, "Invalid JSON format.");
            Py_DECREF(dict);
            free(buffer);
            return NULL;
        }

        *colon_pos = '\0';
        char* key = token;
        char* value = colon_pos + 1;

        // Trim spaces and quotes
        while (*key == ' ' || *key == '"') key++;
        char* key_end = key + strlen(key) - 1;
        while (*key_end == ' ' || *key_end == '"') *(key_end--) = '\0';

        while (*value == ' ' || *value == '"') value++;
        char* value_end = value + strlen(value) - 1;
        while (*value_end == ' ' || *value_end == '"') *(value_end--) = '\0';

        PyObject* py_key = Py_BuildValue("s", key);
        PyObject* py_value = NULL;
        if (strspn(value, "0123456789") == strlen(value)) {
            py_value = Py_BuildValue("i", atoi(value));
        } else {
            py_value = Py_BuildValue("s", value);
        }

        if (!py_key || !py_value || PyDict_SetItem(dict, py_key, py_value) < 0) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to insert key-value pair.");
            Py_XDECREF(py_key);
            Py_XDECREF(py_value);
            Py_DECREF(dict);
            free(buffer);
            return NULL;
        }

        Py_DECREF(py_key);
        Py_DECREF(py_value);
        token = strtok(NULL, ",");
    }

    free(buffer);
    return dict;
}

static PyMethodDef methods[] = {
    {
        "loads",
        cjson_loads,
        METH_VARARGS,
        "load json"
    },
    {
        "dumps",
        cjson_dumps,
        METH_VARARGS,
        "dump json"
    },
    {
        NULL,
        NULL,
        0,
        NULL
    }
};

static struct PyModuleDef utilsmodule = {
    PyModuleDef_HEAD_INIT,
    "cjson",
    NULL,
    -1,
    methods
};

PyMODINIT_FUNC PyInit_cjson(void) {
    return PyModule_Create(&utilsmodule);
}
