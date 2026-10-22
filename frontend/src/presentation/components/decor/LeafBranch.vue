<!-- Leafy branch across the top-right of a card. The .perch marks where the bird's feet land. -->
<script setup lang="ts">
withDefaults(defineProps<{ face?: 'left' | 'right' }>(), { face: 'left' })
</script>

<template>
  <div class="branch" aria-hidden="true">
    <svg viewBox="0 0 300 120"><use href="#branch" width="300" height="120" /></svg>
    <span class="perch" :data-face="face" />
  </div>
</template>

<style scoped>
.branch {
  position: absolute;
  top: -34px;
  right: -18px;
  width: min(62%, 340px);
  pointer-events: none;
}

svg {
  display: block;
  width: 100%;
  height: auto;
  overflow: visible;
}

/* Point on the branch path (x=114, y=60.7 in the 300x120 viewBox) */
.perch {
  position: absolute;
  left: 38%;
  top: 50.5%;
  width: 0;
  height: 0;
}
</style>
