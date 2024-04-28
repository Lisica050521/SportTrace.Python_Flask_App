<script>
    // Скрипт для обработки отправки формы достижений
    window.onload = function() {
        var form = document.getElementById("achievement-form");
        form.addEventListener("submit", function(event) {
            // Обработка пустых полей, замена на "0"
            var inputs = form.getElementsByTagName("input");
            for (var i = 0; i < inputs.length; i++) {
                if (inputs[i].value === "") {
                    inputs[i].value = "0";
                }
            }
        });
    };

    // Парсим данные из Flask в JavaScript
    var data = JSON.parse('{{ data | safe }}');

    // Выводим данные в консоль для проверки
    console.log(data);

    // Конфигурация графика
    var config = {
        type: 'line', // тип графика: линейный
        data: {
            labels: data.dates, // метки по оси X
            datasets: [{
                label: 'Дистанция пробежки',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                data: data.run_distances,
                fill: false,
            }, {
                label: 'Подтягивания',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                data: data.pull_ups,
                fill: false,
            }, {
                label: 'Отжимания',
                backgroundColor: 'rgba(255, 206, 86, 0.2)',
                borderColor: 'rgba(255, 206, 86, 1)',
                data: data.push_ups,
                fill: false,
            }, {
                label: 'Верхний пресс',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                data: data.upper_abs,
                fill: false,
            }, {
                label: 'Нижний пресс',
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                data: data.lower_abs,
                fill: false,
            }, {
                label: 'Подкачка ягодиц',
                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                borderColor: 'rgba(255, 159, 64, 1)',
                data: data.glute_bridges,
                fill: false,
            }]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Прогресс достижений'
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    };

    // Инициализация графика
    var ctx = document.getElementById('plot').getContext('2d');
    var myChart = new Chart(ctx, config);
</script>