#include <Arduino.h>
#include "Page.h"

const char PROGMEM Page::login[] = R"rawliteral(
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход</title>
</head>
<body>
    <h2>Вход в систему</h2>
    <form method="get">
        <label>Логин:</label><br>
        <input type="hidden" name="role" value="log">
        <input type="text" name="username" required><br><br>

        <button type="submit">Войти</button>
    </form>
</body>
</html>
)rawliteral";

const char PROGMEM Page::reload[] = R"rawliteral(
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <!-- Reload every 1 second -->
    <meta http-equiv="refresh" content="1">
    <title>Auto Reload</title>
</head>
<body>
    <p>This page reloads every second.</p>
</body>
</html>)rawliteral";