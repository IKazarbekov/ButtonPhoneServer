#include <Arduino.h>

class Session{
  public:

    /*
    * Checks if a ip exists in session
    *
    * @param ip of client
    * @param pageOrLogin is page if not exists, else name
    * @return true if exists session, else false
    */
    static bool login(const char* ip, const char*& pageOrName);

    /*
    * Append ip and name in array for session
    *
    * @param ip of client
    * @param name of client
    */
    static void reg(const char* ip, const char* name);
/**
 * @brief Returns a formatted string containing all registered usernames
 * 
 * Converts the internal names array to a human-readable format like:
 * ["user1", "user2", "user3"]
 * 
 * @note Caller must free the returned string using Array::freeString()
 * 
 * @return Dynamically allocated string with all names, or "[]" if empty
 */
static const char* allNames();

/**
 * @brief Returns a formatted string containing all registered IP addresses
 * 
 * Converts the internal IPs array to a human-readable format like:
 * ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
 * 
 * @note Caller must free the returned string using Array::freeString()
 * 
 * @return Dynamically allocated string with all IPs, or "[]" if empty
 */
static const char* allIps();

/**
 * @brief Returns a combined string of all names and IPs
 * 
 * @warning ⚠️ DANGER: This method has a critical bug!
 *          Returns a pointer to a local array that goes out of scope.
 *          DO NOT USE - will cause undefined behavior/crashes.
 * 
 * @return Invalid dangling pointer (DO NOT USE)
 * 
 * @deprecated Method is broken. Use allNames() and allIps() separately.
 */
static const char* allUsers();

  private:
    static const int MAXIMUM_USERS = 5;
    static const char* ips[MAXIMUM_USERS];
    static const char* names[MAXIMUM_USERS];
};