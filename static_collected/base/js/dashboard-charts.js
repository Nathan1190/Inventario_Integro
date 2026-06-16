(function() {
  Chart.defaults.global.defaultFontFamily = 'Nunito';
  Chart.defaults.global.defaultFontColor = '#858796';

  var ctxAssign = document.getElementById('assignChart');
  if (ctxAssign) {
    new Chart(ctxAssign, {
      type: 'line',
      data: {
        labels: assignLabels,
        datasets: [{
          label: 'Asignaciones',
          lineTension: 0.3,
          backgroundColor: 'rgba(78, 115, 223, 0.05)',
          borderColor: 'rgba(78, 115, 223, 1)',
          pointRadius: 3,
          pointBackgroundColor: 'rgba(78, 115, 223, 1)',
          pointBorderColor: 'rgba(78, 115, 223, 1)',
          pointHoverRadius: 3,
          pointHoverBackgroundColor: 'rgba(78, 115, 223, 1)',
          pointHoverBorderColor: 'rgba(78, 115, 223, 1)',
          pointHitRadius: 10,
          pointBorderWidth: 2,
          data: assignData
        }]
      },
      options: { maintainAspectRatio: false }
    });
  }

  var ctxCat = document.getElementById('categoryChart');
  if (ctxCat) {
    new Chart(ctxCat, {
      type: 'bar',
      data: {
        labels: categoryLabels,
        datasets: [{
          label: 'Bienes',
          backgroundColor: '#4e73df',
          borderColor: '#4e73df',
          data: categoryData
        }]
      },
      options: { maintainAspectRatio: false }
    });
  }

  var ctxState = document.getElementById('stateChart');
  if (ctxState) {
    new Chart(ctxState, {
      type: 'doughnut',
      data: {
        labels: stateLabels,
        datasets: [{
          data: stateData,
          backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b', '#858796'],
          hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf', '#dda20a', '#be2a2a', '#6c757d'],
          hoverBorderColor: 'rgba(234, 236, 244, 1)'
        }]
      },
      options: { maintainAspectRatio: false, legend: { display: false } }
    });
  }
})();