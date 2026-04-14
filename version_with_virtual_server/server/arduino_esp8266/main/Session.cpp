#include <sys/string.h>
#include <cstring>
#include "Arduino.h"
#include "Session.h"
#include "Array.h"
#include "Page.h"


bool Session::login(const char* ip, const char*& pageOrName)
{
  int index = Array::indexOf(Session::ips, ip);
  if (index != -1)
  {
    pageOrName = Session::names[index];
    return true;
  }
  else
  {
    pageOrName = Page::login;
    return false;
  }
};

void Session::reg(const char* ip, const char* name)
{
  Array::add(Session::ips, Session::MAXIMUM_USERS, ip);
  Array::add(Session::names, Session::MAXIMUM_USERS, name);
};

const char* Session::allNames(){
  return Array::toString(names);
};

const char* Session::allIps(){
  return Array::toString(ips);
};

const char* Session::allUsers(){
  const char* names = Session::allNames();
  const char* ips = Session::allIps();

  char* namesAndUsers = new char[strlen(names) + strlen(ips) + 1];
  strcat(namesAndUsers, names);
  strcat(namesAndUsers, ips);
  return namesAndUsers;
}


const char* Session::names[Session::MAXIMUM_USERS] = {nullptr};
const char* Session::ips[Session::MAXIMUM_USERS] = {nullptr};