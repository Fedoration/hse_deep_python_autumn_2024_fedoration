#include <Python.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

char* concatenate_strings(const char *s1, const char *s2) {
    // Объединение двух строк
    char *char_r = malloc(strlen(s1) + strlen(s2) + 1);
    strcpy(char_r, s1);
    strcat(char_r, s2);
    return char_r;
}

char* from_int_to_char(int number) {
    // Перевести число в char
    char* buffer = malloc(sizeof(char) * 10);
    sprintf(buffer, "%d", number);
    return buffer;
}


PyObject* cjson_dumps(PyObject *self, PyObject *args, PyObject *kwargs) {
        // Дамп данных
        PyObject *dict = NULL, *key = NULL, *value = NULL;
        size_t last = 0;
        if (!PyArg_ParseTuple(args, "O", &dict)) {
                printf("Args must be dict!");
                return NULL;
        }
        char* result = "{";
        Py_ssize_t pos = 0;
        // Проходимся по всем символам и записываем их в строку
        while(PyDict_Next(dict, &pos, &key, &value)) {
                char* _key = PyUnicode_AsUTF8(key);
                if (last != 0 ){
                        _key = concatenate_strings(", \"", _key);
                }
                else {
                        _key = concatenate_strings("\"", _key);

                }
                _key = concatenate_strings(_key, "\": ");
                result = concatenate_strings(result, _key);
                char* _value = NULL;
                if (!PyLong_Check(value)) {
                        _value = PyUnicode_AsUTF8(value);
                        _value = concatenate_strings("\"", _value);
                        _value = concatenate_strings(_value, "\"");
                        result = concatenate_strings(result, _value);
                }
                else {
                        int _value_int = PyLong_AsLong(value);
                        _value = from_int_to_char(_value_int);
                        result = concatenate_strings(result, _value);
                        free(_value);
                }
                last++;
        }
        result = concatenate_strings(result, "}");
        return Py_BuildValue("s", result);
}


PyObject* cjson_loads(PyObject *self, PyObject *args, PyObject *kwargs) {
        // Загрузка данных из дампа
        PyObject *dict = NULL;
        PyObject *key = NULL;
        PyObject *value = NULL;
        int val;
        if (!(dict = PyDict_New())) {
                printf("ERROR: Failed to create Dict Object\n");
                return NULL;
        }
        char *string;
        char *token;
        char *_key;
        char _value[100];
        if (!PyArg_ParseTuple(args, "s", &string)) {
                PyErr_SetString(PyExc_TypeError, "Parameter must be a string!");
                return NULL;
        }
        // Получаем токены с помощью разделителей
        // Проходимся по всем полученных токенам, определяем их как число или строка
        // Сначала извлекаем ключ, затем соответствующее ему значение и записываем пару в словарь
        token = strtok(string, "{\",: }");
        while (token != NULL) {
                _key = token;
                token = strtok(NULL, "{\",: }");
                strcpy(_value, token);
                if (!(key = Py_BuildValue("s", _key))) {
                        printf("Error: fail while extracting string\n");
                        return NULL;
                }
                char *endptr;
                strtol(_value, &endptr, 10);
                if ( *endptr == '\0') {
                        int val = atoi(_value);
                        if (!(value = Py_BuildValue("i", val))) {
                                printf("Error: fail while extracting int\n");
                                return NULL;
                        }
                } else {
                        if (!(value = Py_BuildValue("s", _value))) {
                                printf("Error: fail while extracting int\n");
                                return NULL;
                        }
                }
                if (PyDict_SetItem(dict, key, value) < 0) {
                        printf("Error: fail while set to dict\n");
                        return NULL;
                }
                token = strtok(NULL, "{\",: }");
        }
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
        return PyModule_Create( &utilsmodule);
}