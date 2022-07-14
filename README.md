# Тестовое задание Фабрика-решений
### Создать API для управления рассылками сообщений

### Задачи
- [ ] Разбить проект на модули:
  - [ ] Отделить классы ОРМ моделей
  - [ ] Перенести функции и декораторы
  - [ ] Перенести руты _**(опционально)**_
- [ ] Дописать руты для получения статистики
- [ ] Отказаться от flask-sqlalchemy _**(опционально)**_ и использовать оригинальный sqlalchemy по причинам:
  - Многое не очевидно в реализации flask-sqlalchemy, куцая документация
  - Нет необходимости в использовании фич flask-sqlalchemy
  - Будет проще при вынесении ОРМ классов в отдельный файл
- [ ] Нарисовать схемы функционирования API на draw.io
- [ ] __**Добавить логгирование**__ 

### Глобальные Задачи
- [ ] Написать все необходимые руты
- [ ] Создать сервис, мониторящий дату рассылок и обращающийся к стороннему API для осуществления рассылок
- [ ] Написать документацию
- [ ] Создать админ панель c помощью flask-admin
- [ ] Обернуть в docker-compose

### Завершенные ✓
- [x] Созданы ОРМ модели базы данных
- [x] Созданы схемы валидации marshmallow
- [x] Создан REST API. Реализована часть рутов.