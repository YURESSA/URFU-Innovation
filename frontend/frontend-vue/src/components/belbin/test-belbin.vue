<template>
  <main>
    <div class="test-form">
      <div class="question">
        <h4>{{ test.questions[chapter - 1].block_name }}</h4>
        {{ currentValue }}
      </div>
      <div class="form">
        <div class="form__wrapper">
          <div class="slider" v-for="(item, i) in currentValue" :key="i">
            <belbin-range
            :max="initialMax"
            :min="initialMin"
            :limit="sumPoints(i)"
            v-model:value="item.points"
            :question="questions[i]"
            :index="i"
            @updateRemained="updateRemainedPoints"
            />
            {{ item.points }}
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { computed, defineProps, defineEmits } from 'vue';
import BelbinRange from './belbin-range.vue';

const initialMax = 10;
const initialMin = 0;
const props = defineProps({
  test: Object,
  chapter: Number,
  remainedPoints: Number,
  currentValue: Object,
});

const emit = defineEmits(['updateRemained']);

function sumPoints(except) {
  let sums = 0;
  props.currentValue.forEach((e, i) => {
    if (except !== i) {
      sums += e.points;
    }
  });
  return initialMax - sums;
}

const questions = computed( () =>{
  const currentTest = [...props.test.questions[props.chapter - 1].questions]
  return currentTest
});

const updateRemainedPoints = () => {
  const totalPointsUsed = props.currentValue.reduce((sum, item) => sum + item.points, 0);
  const newRemainedPoints = initialMax - totalPointsUsed;
  emit('updateRemained', newRemainedPoints); 
  
};

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

.slider-container {
  position: relative;
  width: 100%;
  margin-top: 20px;
}
</style>