// Изначальные данные (пустой массив)
let data = [];

// Функция для обновления графика
function updatePlot() {
  // Массивы для хранения данных графика
  const dates = [];
  const pull_ups = [];
  const push_ups = [];
  const upper_abs = [];
  const lower_abs = [];
  const glute_bridges = [];

  // Преобразование данных для Chart.js
  data.forEach((achievement) => {
    dates.push(achievement.date);
    pull_ups.push(achievement.pull_ups);
    push_ups.push(achievement.push_ups);
    upper_abs.push(achievement.upper_abs);
    lower_abs.push(achievement.lower_abs);
    glute_bridges.push(achievement.glute_bridges);
  });

  // Построение графика
  var ctx = document.getElementById('plot').getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: dates, // Используем даты в качестве меток на графике
      datasets: [
        {
          label: 'Подтягивания',
          data: pull_ups,
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1
        },
        {
          label: 'Отжимания',
          data: push_ups,
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        },
        {
          label: 'Верхний пресс',
          data: upper_abs,
          borderColor: 'rgba(255, 206, 86, 1)',
          borderWidth: 1
        },
        {
          label: 'Нижний пресс',
          data: lower_abs,
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        },
        {
          label: 'Подкачка ягодиц',
          data: glute_bridges,
          borderColor: 'rgba(153, 102, 255, 1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          }
        }]
      }
    }
  });
}

// Функция для добавления новых данных
function addData(newAchievements) {
  // Преобразование даты и добавление новых данных в массив
  newAchievements.forEach((newAchievement) => {
    // Создаем объект с данными
    const achievementData = {
      date: newAchievement.date,
      pull_ups: newAchievement.pull_ups,
      push_ups: newAchievement.push_ups,
      upper_abs: newAchievement.upper_abs,
      lower_abs: newAchievement.lower_abs,
      glute_bridges: newAchievement.glute_bridges
    };

    // Добавляем данные в массив
    data.push(achievementData);
  });

  // Удаление текущего графика
  removeChart();

  // Обновление графика
  updatePlot();
}

// Функция для удаления текущего графика
function removeChart() {
  var chartElement = document.getElementById('plot');
  var chartContext = chartElement.getContext('2d');
  chartContext.clearRect(0, 0, chartElement.width, chartElement.height);
}

function logData() {
  console.log(data);
}

// Пример использования:
// Предположим, что у вас есть массив с данными achievements, полученными из таблицы.
// Вы можете передавать этот массив в функцию addData для отображения на графике.
const achievements = []; // Ваш массив данных, который будет вводить пользователь
addData(achievements);

logData();