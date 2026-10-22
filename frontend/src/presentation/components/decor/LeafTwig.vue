<!-- Small twig on a card edge. The .perch marks where the bird's feet land. -->
<script setup lang="ts">
withDefaults(
  defineProps<{
    placement?: 'left' | 'right' | 'center'
    face?: 'left' | 'right'
  }>(),
  { placement: 'left', face: 'right' },
)
</script>

<template>
  <div class="twig" :class="`twig--${placement}`" aria-hidden="true">
    <svg viewBox="0 0 160 60"><use href="#twig" width="160" height="60" /></svg>
    <span class="perch" :data-face="face" />
  </div>
</template>

<style scoped>
.twig {
  position: absolute;
  top: -26px;
  width: 150px;
  pointer-events: none;
}

.twig--left { left: -14px; }
.twig--right { right: -14px; transform: scaleX(-1); }
.twig--center { position: relative; top: auto; width: 130px; margin: 0 auto .5rem; }

svg {
  display: block;
  width: 100%;
  height: auto;
  overflow: visible;
}

/* Point on the twig path (x=53, y=32.3 in the 160x60 viewBox) */
.perch {
  position: absolute;
  left: 33%;
  top: 54%;
  width: 0;
  height: 0;
}
</style>
