<template>
  <div class="stat-container">
    <div class="stat-item left-image animate--slow">
      <img :src="stat.image" class="flip stat-inner-image" />
    </div>
    <div class="stat-item right-image animate--slow">
      <img :src="stat.image" class="stat-inner-image" />
    </div>
    <div class="stat-item stat-text animate--slow animate--delay">
      <h1 class="stat-inner-text" v-html="stat.text"></h1>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { StatData } from "@/models";

export default defineComponent({
  name: "StatDisplay",
  props: {
    stat: {
      type: Object as () => StatData,
      required: true,
    },
  },
});
</script>

<style lang="css" scoped>
body {
  /* just here to make working on it easier */
  background-color: black;
  margin-top: 10vh;
  display: grid;
  place-items: center;
}

.stat-container {
  /* allow children to stack */
  margin: 0px;
  height: 40vmin;
  width: 80vmin;
  /* center content */
  align-items: center;
  justify-content: center;
  position: relative;
}

.stat-item {
  /* allow children to stack */
  position: absolute;
  height: 100%;
}

.stat-inner-image {
  height: 100%;
}

.stat-inner-text {
  font-size: 3vmin;
  padding: 10px;
  color: black;
  overflow-wrap: normal;
  /* center text horizonally and vertically */
  text-align: center;
  width: 50%;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  border: 0.5vmin solid rgb(0, 0, 0);
}

@keyframes slideInLeft {
  0% {
    opacity: 0;
    transform: translateX(-100px);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  0% {
    opacity: 0;
    transform: translateX(100px);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInBottom {
  0% {
    opacity: 0;
    transform: translateY(100px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate--slow {
  animation-duration: 1s;
}

.animate--delay {
  animation-delay: 1s;
}

.stat-text {
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  animation-name: slideInBottom;
  animation-fill-mode: both;
}

.right-image {
  right: 0px;
  animation-name: slideInRight;
}

.flip {
  transform: scaleX(-1);
}

.left-image {
  left: 0px;
  animation-name: slideInLeft;
}
</style>
