<template>
  <p>{{ index+1 }}. {{ question }}</p>
  <div class="slider-container">
    <div class="value-labes">
      <span v-for="num in 11" :key="num" class="label-mark">
        <span 
          class="slider-value__wrapper" 
          ref="labelsMark" 
          :class="{
            'mobile-start-label-value': num >= 0 && num <= 3,
            'mobile-mid-label-value': num >= 6 && num <= 8,
            'mobile-end-label-value': num >= 9 && num <= 10
          }"
        >
          <span class="slider-value">{{ dataV }}</span>
        </span>
      </span>
    </div>
    <input
      type="range"
      ref="slider"
      class="slider"
      :class="{ 'slider-active': isHoveringThumb }"
      :min="min"
      :max="max"
      v-model="dataV"
      @input="onInput"
      @mousedown="onMouseDown"
      @mouseup="onMouseUp"
      @touchstart="onMouseDown"
      @touchend="onMouseUp"
    />
    <div class="slider-labels">
      <span v-for="num in 11" :key="num" class="label">
        <span :class="{'bold': num-1 == 0}" ref="valueLabel">{{ num - 1 }}</span>
        <span class="mark-position"></span>
      </span>
    </div>
    {{ leftValue }}
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

const dataV = ref(props.value || 0);
const slider = ref(null);
const limitRef = toRef(props, 'limit');
const isHoveringThumb = ref(false);
const leftValue = ref();
const labelsMark = ref([]);
const valueLabel = ref([]);

labelsMark.value.forEach((item) => {
  item.classList.remove('label-active');
});

onMounted(() => {
  if (slider.value) {
    slider.value.style.background = `linear-gradient(to right, #57C0CF 100%, #a6a6a6 0%)`;
  }
});

const onMouseDown = () => {
  isHoveringThumb.value = true
  const label = labelsMark.value[dataV.value];
  label.classList.add('label-active');
};

const onMouseUp = () => {
  isHoveringThumb.value = false
  const label = labelsMark.value[dataV.value];
  label.classList.remove('label-active');
};

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
    slider.value.style.background = `linear-gradient(to right, #57C0CF ${gradientValue}, #c2c2c2 ${gradientValue}, #c2c2c2 100%)`;
  }
});

const lastNumber = ref(0)

const updateSliderValue = () => {

  labelsMark.value.forEach((item) => {
    item.classList.remove('label-active');
  });
  const label = labelsMark.value[dataV.value];
  const labelValue = valueLabel.value[dataV.value]
  const numberNow = parseInt(labelValue.innerHTML.trim());
  if(numberNow > lastNumber.value){
    labelValue.style.fontWeight = '600'
  } else {
    labelValue.style.fontWeight = '500'
    valueLabel.value[dataV.value+1].style.fontWeight = '500'
  }
  if (label) {
    label.classList.add('label-active');
  }
  lastNumber.value = numberNow
};


function onInput(e){
  const current = Number(e.target.value);
  if (current <= props.limit) {
    dataV.value = current;
    updateSliderValue();
  } else{
    dataV.value = props.limit
  }
  emit('update:value', dataV.value)
  emit('updateRemained')
}

</script>

<style scoped>

.mark-position{
  display: block;
  position: absolute;
  width: 2px;
  height: 7px;
  background-color: #A6A6A6;
  left: 2px;
  top: -23px;
  z-index: 1;
}

.slider {
  -webkit-appearance: none;
  width: 100%;
  height: 2px;
}

.slider-container{
  position: relative;
  width: 100%;
}

.bold{ 
  font-weight: 600;
}

.slider-value__wrapper{
  position: absolute;
  top: -37px;
  left: -13px;
  width: 32px;
  height: 32px;
  display: none;
  transform: rotate(-45deg);
  align-items: center;
  border-radius: 50% 50% 50% 0;
  justify-content: center;
  background-color: #57c0cf;
}

.label-active{
  display: flex;
}

.slider-value{
  /* color: #fff; */
  font-weight: 600;
  transform: rotate(45deg);
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  background: #57c0cf;
  cursor: pointer;
  border-radius: 50%;
  margin-top: -6px;
  box-shadow: 0px 0px 0px 6px rgba(53, 151, 167, 0.16);
  transition: box-shadow 0.3s ease;
  position: relative; /* Чтобы задать контекст позиционирования */
  z-index: 10; /* Убедитесь, что значение z-index достаточно высокое */
}

.slider-active::-webkit-slider-thumb{
  box-shadow: 0px 0px 0px 10px rgba(53, 151, 167, 0.16);
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
  margin-top: 14px;
  padding-left: 1%;
  width: 99%;
  position: relative;
}

.value-labes{
  display: flex;
  justify-content: space-between;
  margin-top: 14px;
  padding-left: 1%;
  width: 98%;
}

.label, .label-mark {
  font-size: 14px;
  color: #333;
  position: relative;
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
  .mobile-start-label-value{
    left: -9px;
  }
  .mobile-mid-label-value{
    left: -17px;
  }
  .mobile-end-label-value{
    left: -20px;
  }
}
</style>