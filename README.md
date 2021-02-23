![](https://raw.githubusercontent.com/maksimio/Video-Creator/master/img/logo3.1.png)

# Video Creator 🎬
Данный репозиторий посвящен аддону для 3D-редактора [Blender](https://www.blender.org) версии 2.91.2 (_проверено, также работает на 2.83; работоспособность на других версиях не тестировалась_). Этот аддон позволяет автоматически сгенерировать 3D видео с геометрическими объектами, информация о которых передается в специальном json-файле. Файл с данными должен иметь определенную структуру.

Назначение аддона: автоматическая визуализация в формате 3D Side-by-Side (стереопара) сложных механических/информационных процессов на основании входного json-файла. Он будет полезен людям, связанным с научными разработками, статистикой, информационными технологиями, так как позволит наглядно демонстрировать результаты экспериментов и наблюдений, а также различные модели.

> Для установки стабильной версии аддона используйте раздел _release_.

## Структура репозитория
1. addon - главная директория, непосредственно сам аддон. Может быть использован отдельно.
1. developments - экспериментальные наработки по теме проекта.
1. generators - специальные генераторы json файлов. Работают отдельно от аддона.
1. img - место хранения изображений (в т.ч. для Wiki)
1. jsonfiles - примеры json-файлов. Можно использовать для тестирования аддона, открывая их через.

# Примеры 🎥
Примеры входных файлов в формате json, которые обрабатывает аддон размещены в папке _jsonfiles_. Примеры отрендеренных видео с использованием аддона и соответствующих файлов для их рендера можно найти [здесь](https://drive.google.com/drive/folders/1CDenA3h9r8XsHT7CZwCwW7Wp1E45tlFN?usp=sharing).

# Wiki 📃
Вся структурированная документация с изображениями содержится в [Wiki](https://github.com/maksimio/Video-Creator/wiki) этого репозитория. Там вы найдете информацию об установке аддона в Blender, о структуре формата входных данных, руководство по использованию и т.д.

# Contributors ✨
На начальных этапах разработка велась в черновом приватном репозитории.

Этот проект был подготовлен в рамках дисциплины ОПД Санкт-Петербургского Политехнического университета весной 2020 года. Команда проекта состояла из 4-х человек, во главе с руководителем проекта (владелец этого репозитория). Каждый из участников команды внес неоценимый вклад в развитие проекта. Вот они слева направо:
<table>
  <tr>
    <td align="center"><a href="https://github.com/maksimio"><img src="https://avatars0.githubusercontent.com/u/61945327?s=460&u=acf5d9982b5445ff5ee0dded836ff402d90f1dea&v=4" width="100px;" alt=""/><br /><sub><b>Максим</b></sub></a><br /><a href="#Contributors" title="Project Management">📆</a> <a href="#Contributors" title="Code">💻</a> <a href="#Contributors" title="Design">🎨</a> <a href="#Contributors" title="Documentation">📖</a></td>
        <td align="center"><a href="https://github.com/Karablik"><img src="https://avatars2.githubusercontent.com/u/62114626?s=460&u=840b078909a98689f02837551a4cca1ed2e6267a&v=4" width="100px;" alt=""/><br /><sub><b>Данила</b></sub></a><br /><a href="#Contributors" title="Code">💻</a> <a href="#Contributors" title="Ideas & Planning">🤔</a> <a href="#Contributors" title="Examples">💡</a> <a href="#Contributors" title="Videos">📹</a></td>
        <td align="center"><a href="https://github.com/dew8"><img src="https://avatars0.githubusercontent.com/u/62108895?s=460&u=16f99935601515fd777fd3080bba9814e66825cd&v=4" width="100px;" alt=""/><br /><sub><b>Ирэна</b></sub></a><br /><a href="#Contributors" title="Code">💻</a> <a href="#Contributors" title="Content">🖋</a> <a href="#Contributors" title="Talks">📢</a> <a href="#Contributors" title="User Testing">📓</a></td>
        <td align="center"><a href="https://github.com/AnatoliyBr"><img src="https://avatars0.githubusercontent.com/u/62114392?s=460&u=d42d2ae93128d46acb2570e9613c7ba0a2b3e9a1&v=4" width="100px;" alt=""/><br /><sub><b>Анатолий</b></sub></a><br /><a href="#Contributors" title="Code">💻</a> <a href="#Contributors" title="Answering Questions">💬</a> <a href="#Contributors" title="Tools">🔧</a> <a href="#Contributors" title="Blogposts">📝</a></td>
  </tr>
</table>

# Защита проекта

С итоговой презентацией по теме проекта и конспектом можно ознакомиться [здесь](https://maksimio.github.io/videoCreator/).

***

# Обратная связь 📬
Если у вас появились вопросы по проекту и вы хотите обсудить их, то кроме Issues вы можете связаться с нами по электронной почте:

* Максим: maksim.lopatin.spb@mail.ru, lopatin.ma@edu.spbstu.ru
* Данила: savin.dd@edu.spbstu.ru
* Ирэна: gureeva.im@edu.spbstu.ru
* Анатолий: bryushinin.aa@edu.spbstu.ru
