const weatherData = {
  northern: {
    temp: '62°F',
    condition: 'Cool with crisp air in the hills.',
    advice: 'Bring a warm layer and expect shaded, mossy paths.'
  },
  central: {
    temp: '68°F',
    condition: 'Mild with scattered clouds.',
    advice: 'Perfect for a midday hike; pack water and trail snacks.'
  },
  southern: {
    temp: '72°F',
    condition: 'Sunny near the shore with light breeze.',
    advice: 'Wear sunscreen and keep extra hydration on hand.'
  },
  western: {
    temp: '60°F',
    condition: 'Cool and calm with wooded scenery.',
    advice: 'A light jacket helps on the ridge and in shaded areas.'
  }
};

function updateWeather() {
  const select = document.getElementById('region-select');
  if (!select) return;

  const region = select.value;
  const data = weatherData[region];
  document.getElementById('temp').textContent = data.temp;
  document.getElementById('condition').textContent = data.condition;
  document.getElementById('advice').textContent = data.advice;
}

window.addEventListener('DOMContentLoaded', () => {
  const select = document.getElementById('region-select');
  if (select) {
    select.addEventListener('change', updateWeather);
    updateWeather();
  }
});
