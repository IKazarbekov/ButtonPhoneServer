#include "Array.h"

bool Array::contains(const char* array[], const char* value) {
    if (!array || !value) return false;
    
    for (int i = 0; array[i] != nullptr; i++) {
        if (strcmp(array[i], value) == 0) {
            return true;
        }
    }
    return false;
}

bool Array::contains(const char* array[], int size, const char* value) {
    if (!array || !value || size <= 0) return false;
    
    for (int i = 0; i < size; i++) {
        if (array[i] && strcmp(array[i], value) == 0) {
            return true;
        }
    }
    return false;
}

int Array::indexOf(const char* array[], const char* value) {
    if (!array || !value) return -1;
    
    for (int i = 0; array[i] != nullptr; i++) {
        if (strcmp(array[i], value) == 0) {
            return i;
        }
    }
    return -1;
}

int Array::indexOf(const char* array[], int size, const char* value) {
    if (!array || !value || size <= 0) return -1;
    
    for (int i = 0; i < size; i++) {
        if (array[i] && strcmp(array[i], value) == 0) {
            return i;
        }
    }
    return -1;
}

bool Array::add(const char* array[], int maxSize, const char* value) {
    // Debug
    

    // Find first empty slot
    for (int i = 0; i < maxSize - 1; i++) {
        if (array[i] == nullptr) {
            array[i] = value;
            array[i + 1] = nullptr;  // Ensure null termination
            return true;
        }
    }
    return false;  // No space
}

const char* Array::toString(const char* array[]) {
    int count = 0;
    while (array[count] != nullptr) {
        count++;
    }
    
    return toString(array, count);
}

const char* Array::toString(const char* array[], int size) {
    if (size == 0) {
        char* result = new char[3];
        strcpy(result, "[]");
        return result;
    }
    
    // Вычисляем необходимый размер буфера
    int totalLength = 2; // для [] и запятых
    
    for (int i = 0; i < size; i++) {
        if (array[i] != nullptr) {
            totalLength += strlen(array[i]) + 2; // +2 для кавычек
        } else {
            totalLength += 4; // "null"
        }
        if (i < size - 1) {
            totalLength += 2; // ", "
        }
    }
    
    // Выделяем память
    char* buffer = new char[totalLength + 1];
    char* ptr = buffer;
    
    ptr += sprintf(ptr, "[");
    
    for (int i = 0; i < size; i++) {
        if (i > 0) {
            ptr += sprintf(ptr, ", ");
        }
        
        if (array[i] == nullptr) {
            ptr += sprintf(ptr, "null");
        } else {
            ptr += sprintf(ptr, "\"%s\"", array[i]);
        }
    }
    
    ptr += sprintf(ptr, "]");
    
    return buffer;
}