<template>
  <div class="slide-show-container">
    <div class="stat-container">
      <StatDisplay :stat="stats[current]" :key="current" />
    </div>
  </div>
  <div class="button-panel">
    <button @click="prev"><font-awesome-icon icon="left-long" /></button>
    <button @click="next"><font-awesome-icon icon="right-long" /></button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import StatDisplay from "@/components/StatDisplay.vue";

let defaultStats = [
  {
    image: "https://oldschool.runescape.wiki/images/Hans.png?1a5c5",
    text: "You've played for:<br /> 2080 hours<br />That's a full working year!",
  },
  {
    image: "https://oldschool.runescape.wiki/images/Goblin.png?3e49a",
    text: "Your most killed mob is:<br />Goblin (lvl 3)<br />with 42069 kills!",
  },
  {
    image:
      "https://oldschool.runescape.wiki/images/Grand_Exchange_pillar.png?90523",
    text: "Your favourite location is:<br />The Grand Exchange<br />with 703 visits<br />Totalling 803 hours!",
  },
  {
    image:
      "https://oldschool.runescape.wiki/images/Rock_golem_%28follower%29.png?269fc",
    text: "Your favourite skill is:<br />Mining<br />with 42069 xp gained",
  },
];

// pull stats from /api/v1/wrapped?username=jerome
// if it fails, use default stats

export default defineComponent({
  name: "StatSlideShow",
  components: {
    StatDisplay,
  },
  data() {
    return {
      current: 0,
      stats: defaultStats,
    };
  },
  methods: {
    next() {
      this.current = (this.current + 1) % this.stats.length;
    },
    prev() {
      this.current = (this.current - 1 + this.stats.length) % this.stats.length;
    },
  },
  async mounted() {
    this.stats = await fetch("/api/v1/wrapped?username=jerome")
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        return data;
      })
      .catch((error) => {
        console.error("Error:", error);
        return defaultStats;
      });
  },
});
</script>

<style lang="css" scoped>
.slide-show-container {
  /* center content */
  align-items: center;
  justify-content: center;
  position: relative;
}

.button-panel {
  width: 50%;
  display: flex;
  justify-content: center;
  margin-top: 8vmin;
  display: flex;
  justify-content: space-around;
}

.button-panel > button {
  background-color: transparent;
  border: 0.5vmin solid rgb(0, 0, 0);
  border-radius: 100%;
  font-size: 5vmin;
  color: black;
  cursor: pointer;
  transition: 0.3s;
  font-size: 5vmin;
  height: 15vmin;
  width: 15vmin;
}
</style>
