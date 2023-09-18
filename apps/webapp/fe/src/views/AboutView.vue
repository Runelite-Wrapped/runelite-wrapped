<template>
  <div class="about">
    <img
      alt="Vue logo"
      src="../assets/runelite_wrapped_icon_wide.png"
      class="top-image"
    />
    <h1>Runelite Wrapped</h1>
    <p>
      Runelite Wrapped is an open source app that provide OSRS users (who play
      with runelite) the ability to get a year summary of their OSRS gaming
      similar to
      <a href="https://newsroom.spotify.com/2022-wrapped/" target="_blank"
        >Spotify Wrapped</a
      >
    </p>
    <h2>Source Code</h2>
    <p>
      View on github
      <a
        href="https://github.com/Runelite-Wrapped/runelite-wrapped"
        target="_blank"
        >here</a
      >
    </p>
    <h2>Authors</h2>
    <p>
      Sam Kyle<br />
      <a href="https://github.com/Samueljbk" target="_blank">GitHub</a>
    </p>
    <p>
      Jerome Swannack <br />
      <a href="https://github.com/jerome3o" target="_blank">GitHub</a>
    </p>
  </div>
</template>

<style scoped>
.about {
  display: grid;
  place-items: center;
  margin-top: 1vh;
  width: 50%;
  /* make centered on page */
  margin-left: auto;
  margin-right: auto;
}
.top-image {
  width: 40%;
  top: 0;
  left: 0;
}
</style>
