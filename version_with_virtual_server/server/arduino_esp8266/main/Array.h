#ifndef ARRAY_H
#define ARRAY_H

#include <Arduino.h>

class Array {
public:
    /**
     * Checks if a value exists in a null-terminated array of strings
     * @param array Array of strings terminated by nullptr
     * @param value Value to search for
     * @return true if found, false otherwise
     */
    static bool contains(const char* array[], const char* value);
    
    /**
     * Checks if a value exists in an array with known size
     * @param array Array of strings
     * @param size Size of the array
     * @param value Value to search for
     * @return true if found, false otherwise
     */
    static bool contains(const char* array[], int size, const char* value);

    /**
     * Finds the index of a value in a null-terminated array of strings
     * @param array Array of strings terminated by nullptr
     * @param value Value to search for
     * @return Index of the value if found, -1 otherwise
     */
    static int indexOf(const char* array[], const char* value);
    
    /**
     * Finds the index of a value in an array with known size
     * @param array Array of strings
     * @param size Size of the array
     * @param value Value to search for
     * @return Index of the value if found, -1 otherwise
     */
    static int indexOf(const char* array[], int size, const char* value);

        /**
     * Adds an element to a null-terminated array
     * @param array Array of strings terminated by nullptr (will be modified)
     * @param maxSize Maximum size of the array (including nullptr terminator)
     * @param value Value to add
     * @return true if added successfully, false if array is full
     */
    static bool add(const char* array[], int maxSize, const char* value);

    /**
     * Converts null-terminated array to readable string
     * @param array Array of strings terminated by nullptr
     * @return Dynamically allocated string (must be freed with freeString())
     */
    static const char* toString(const char* array[]);
    
    /**
     * Converts array with known size to readable string
     * @param array Array of strings
     * @param size Size of the array
     * @return Dynamically allocated string (must be freed with freeString())
     */
    static const char* toString(const char* array[], int size);

};

#endif