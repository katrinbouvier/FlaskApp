Feature: Проверка авторизации
Scenario: Проверить, что поле ввода пустое
  Given website "127.0.0.1:5000"
  Then push button with text 'ВОЙТИ'
  Then page include text 'В поле ничего нет'