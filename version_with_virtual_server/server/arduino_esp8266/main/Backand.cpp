#include <sys/string.h>
#include <Arduino.h>
#include "Backand.h"
#include "Session.h"
#include "Page.h"


const char* Backand::main_processing_request(const char* input_data){
  // get argument by separator ";"
  char buffer[strlen(input_data) + 1];
  strcpy(buffer, input_data);
  char* saveptr;
  char* arg1_ip = strtok_r(buffer, ";", &saveptr);
  char* arg2_command = strtok_r(NULL, ";", &saveptr);
  char* arg3_name = strtok_r(NULL, ";", &saveptr);

  // send all users
  if (strcmp(arg2_command, "debug_info") == 0)
  {
    return Session::allUsers();
  }

  // login or register
  const char* pageOrName;
  if (!Session::login(arg1_ip, pageOrName)){
    if (strcmp(arg2_command, "log") == 0)
    {
      Session::reg(arg1_ip, arg3_name);
      return Page::reload;
    }
    return pageOrName;
  }

  return pageOrName;
};