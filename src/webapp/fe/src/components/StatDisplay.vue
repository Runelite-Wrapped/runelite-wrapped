<template>
  <div class="stat-container">
    <div class="stat-item left-image animate--slow">
      <img
        src="https://oldschool.runescape.wiki/images/Hans.png?1a5c5"
        class="flip stat-inner-image"
      />
    </div>
    <div class="stat-item right-image animate--slow">
      <img
        src="https://oldschool.runescape.wiki/images/Hans.png?1a5c5"
        class="stat-inner-image"
      />
    </div>
    <div class="stat-item stat-text animate--slow animate--delay">
      <h1 class="stat-inner-text">You've played for:<br />100 hours</h1>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "StatDisplay",
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
  height: 500px;
  width: 500px;
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
  margin: 0px;
  color: black;
  overflow-wrap: normal;
  /* center text horizonally and vertically */
  text-align: center;
  width: 50%;
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
