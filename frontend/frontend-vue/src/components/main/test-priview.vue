<template>
  <div class="test">
    <img src="@public/assets/main-page/belbin-preview.svg" class="test-img" alt="">
    <h2>{{ title }}</h2>
    <img src="@public/assets/main-page/star2.svg" class="star" alt="Star" />
  </div>
</template>

<script setup>
const props = defineProps({
  title: String,
})
</script>

<style scoped>
.test {
  display: flex;
  justify-content: left;
  align-items: center;
  background-color: #67DDDC;
  border-radius: 7px;
  width: 300px;
  height: 180px;
  padding: 27px 31px;
  position: relative;
  cursor: pointer;
  transition: 0.5s all ease;
}

.test-img{
  position: absolute;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: 0.5s all ease;
}

.test:hover{
  background-color: rgb(92, 245, 242);
}

.test:hover .test-img{
  opacity: 1;
}

.test:hover h2, 
.test:hover .star{
  opacity: 0;
}

h2{
  font-size: 64px;
  font-weight: 500;
  width: 100px;
  transition: 0.3s all ease;
}

.star {
  position: absolute;
  top: 0px;
  right: 0px;
  transition: 0.3s all ease;
  height: 150px;
}

@media screen and (max-width: 980px) {
  .star{
    width: 150px;
  }
  .test{
    width: 250px;
  }
}
</style>
