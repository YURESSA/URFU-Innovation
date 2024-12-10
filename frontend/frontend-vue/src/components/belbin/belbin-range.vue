<template>
  <p>{{ index+1 }}. {{ question }}</p>
  <div class="slider-container">
    <input
      type="range"
      ref="slider"
      class="slider"
      :min="min"
      :max="max"
      v-model="dataV"
      @input="onInput"
    />
    <div class="slider-labels">
      <span v-for="num in 11" :key="num" class="label">{{ num - 1 }}</span>
    </div>
  </div>
</template>

<script setup>
import { defineProps, ref, defineEmits, watch, toRef, onMounted } from 'vue';

const emit = defineEmits(['update:value', 'updateRemained'])

const props = defineProps({
  max: Number,
  min: Number,
  limit: {
    type: Number,
    default: 10,
  },
  value: Number,
  question: String,
  index: Number,
})

const dataV = ref(props.value || 0)
const slider = ref(null);
const limitRef = toRef(props, 'limit');

onMounted(() => {
  if (slider.value) {
    slider.value.style.background = `linear-gradient(to right, #57C0CF 100%, #a6a6a6 0%)`;
  }
});

watch(
  () => props.value,
  (newValue) => {
    dataV.value = newValue;
    emit('updateRemained')
  }
);

watch(limitRef, (newValue) => {
  if (slider.value) {
    let gradientValue;
    if (newValue == 9 || newValue == 8) {
      gradientValue = `${newValue * 10 - 1}%`;
    } else if (newValue == 2 || newValue == 1) {
      gradientValue = `${newValue * 10 + 1}%`;
    } else {
      gradientValue = `${newValue * 10}%`;
    }
    slider.value.style.background = `linear-gradient(to right, #57C0CF ${gradientValue}, #a6a6a6 0%)`;
  }
});

function onInput(e){
  const current = Number(e.target.value);
  if (current <= props.limit) {
    dataV.value = current;
  } else{
    dataV.value = props.limit
  }
  emit('update:value', dataV.value)
  emit('updateRemained')
}

</script>

<style scoped>
.slider {
  -webkit-appearance: none;
  width: 100%;
  height: 3px;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 25px;
  height: 25px;
  background: #57c0cf;
  border: 1px solid #2b2a28;
  cursor: pointer;
  border-radius: 50%;
  margin-top: -11px;
}

.slider::-webkit-slider-runnable-track {
  width: 100%;
  height: 4px;
  background: none;
  border-radius: 5px;
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

@media screen and (max-width: 600px) {
  .slider::-webkit-slider-thumb {
    width: 20px;
    height: 20px;
    margin-top: -7px;
  }
  .slider::-webkit-slider-runnable-track {
    width: 100%;
    height: 3px;
  }
  .slider-labels {
    padding-left: 3%;
  }
}
</style>