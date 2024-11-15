<template>
  <main>
    <div class="test-form">
      <div class="question">
        <h4>{{ test.questions[charapter - 1].block_name }}</h4>
      </div>
      <div class="form">
        <form ref="testForm" method="post">
          <div class="form__wrapper" v-for="(item, i) in test.questions[charapter - 1].questions" :key="i">
            <p>{{ i+1 }}. {{ item }}</p>
            <div class="slider-container">
              <input
                type="range"
                min="0"
                step="1"
                value="0"
                :max="maxSliderValue(i)"
                v-model.number="sliderValues[i]"
                class="slider"
                :ref="'slider' + i"
                @input="updateMax(i)"
              />
              <div class="slider-labels">
                <span v-for="num in 11" :key="num" class="label">{{ num - 1 }}</span>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </main>
</template>

<script setup>
import {computed, defineEmits, defineProps, reactive} from 'vue';

const initialMax = 10;
const props = defineProps({
  test: Array,
  charapter: Number
});
const emit = defineEmits(['updateRemainingPoints', 'updateSliderValues']);

const sliderValues = reactive(Array(props.test.questions[props.charapter - 1].questions.length).fill(0));

// Вычисление оставшихся баллов
const remainingPoints = computed(() => {
  const total = sliderValues.reduce((acc, val) => acc + val, 0);
  return initialMax - total;
});

// Метод для вычисления максимального значения слайдера
function maxSliderValue(index) {
  // Если оставшихся баллов 0, то не даем увеличивать значение слайдера
  if (remainingPoints.value <= 0 && sliderValues[index] < initialMax) {
    return sliderValues[index]; // Запрещаем увеличение слайдера
  }
  return initialMax; // Разрешаем максимальное значение слайдера, если есть баллы
}

// Обновление значений слайдера и оставшихся баллов
function updateMax(index) {
  // Если оставшихся баллов меньше 0, ограничиваем уменьшение
  if (remainingPoints.value < 0) {
    sliderValues[index] -= 1; // Корректировка значения слайдера
  }

  // Обновляем оставшиеся баллы и значения слайдеров
  emit('updateRemainingPoints', remainingPoints.value);
  emit('updateSliderValues', sliderValues);
}
</script>

<style scoped>
input {
  width: 100%;
}

.test-form {
  width: 50%;
}

main {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.question h4 {
  font-weight: 900;
}

.slider {
  -webkit-appearance: none;
  width: 100%;
  height: 3px;
  background: #490707;
  outline: none;
  border-radius: 5px;
}

.slider-container {
  position: relative;
  width: 100%;
  margin-top: 20px;
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  padding-left: 1%;
}

.label {
  font-size: 12px;
  color: #333;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  background: #57c0cf;
  border: 1px solid #2b2a28;
  cursor: pointer;
  border-radius: 50%;
  margin-top: -7px;
}

.slider::-webkit-slider-runnable-track {
  width: 100%;
  height: 3px;
  background: #a6a6a6;
  border-radius: 5px;
}
</style>