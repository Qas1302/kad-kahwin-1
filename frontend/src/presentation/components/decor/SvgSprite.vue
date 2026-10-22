<!-- Shared SVG shapes (leaf, blossom, branch, twig) referenced with <use href="#..."> -->
<template>
  <svg class="sprite" aria-hidden="true" focusable="false">
    <defs>
      <path id="leaf" d="M0 0 C6 -7 18 -7 24 0 C18 7 6 7 0 0 Z" />
      <g id="blossom">
        <circle cx="0" cy="-5" r="4.6" />
        <circle cx="4.8" cy="-1.6" r="4.6" />
        <circle cx="3" cy="4.1" r="4.6" />
        <circle cx="-3" cy="4.1" r="4.6" />
        <circle cx="-4.8" cy="-1.6" r="4.6" />
        <circle r="2.6" fill="#f3cf86" />
      </g>

      <symbol id="branch" viewBox="0 0 300 120">
        <g fill="none" stroke="#bfa58f" stroke-linecap="round">
          <path d="M300 20 C240 30 200 50 150 58 S60 70 10 66" stroke-width="5" />
          <path d="M212 46 C216 60 222 72 232 80" stroke-width="2.5" />
          <path d="M72 67 C64 78 58 90 58 102" stroke-width="2.5" />
        </g>
        <use href="#leaf" transform="translate(286 22) rotate(-120)" fill="#a9d1b3" />
        <use href="#leaf" transform="translate(266 26) rotate(105)" fill="#c2e3c8" />
        <use href="#leaf" transform="translate(242 32) rotate(-150)" fill="#93c2a1" />
        <use href="#leaf" transform="translate(198 50) rotate(-165) scale(.9)" fill="#a9d1b3" />
        <use href="#leaf" transform="translate(180 53) rotate(115) scale(.9)" fill="#c2e3c8" />
        <use href="#leaf" transform="translate(232 80) rotate(75) scale(.85)" fill="#93c2a1" />
        <use href="#leaf" transform="translate(220 64) rotate(160) scale(.8)" fill="#a9d1b3" />
        <use href="#leaf" transform="translate(224 68) rotate(20) scale(.8)" fill="#c2e3c8" />
        <use href="#leaf" transform="translate(58 102) rotate(95) scale(.85)" fill="#a9d1b3" />
        <use href="#leaf" transform="translate(62 84) rotate(165) scale(.8)" fill="#93c2a1" />
        <use href="#leaf" transform="translate(64 88) rotate(15) scale(.8)" fill="#c2e3c8" />
        <use href="#leaf" transform="translate(42 68) rotate(-150) scale(.9)" fill="#a9d1b3" />
        <use href="#leaf" transform="translate(24 67) rotate(160) scale(.9)" fill="#c2e3c8" />
        <use href="#leaf" transform="translate(12 66) rotate(-175) scale(.8)" fill="#93c2a1" />
        <use href="#blossom" transform="translate(254 38)" fill="#f6cbd1" />
        <use href="#blossom" transform="translate(206 56) scale(.8)" fill="#e6dcf5" />
        <use href="#blossom" transform="translate(84 60) scale(.85)" fill="#fde0cb" />
        <use href="#blossom" transform="translate(32 76) scale(.75)" fill="#f6cbd1" />
        <use href="#blossom" transform="translate(234 90) scale(.7)" fill="#f6cbd1" />
      </symbol>

      <symbol id="twig" viewBox="0 0 160 60">
        <g fill="none" stroke="#bfa58f" stroke-linecap="round">
          <path d="M2 40 C40 34 90 30 158 36" stroke-width="4" />
          <path d="M118 33 C126 25 134 21 144 19" stroke-width="2.2" />
        </g>
        <use href="#leaf" transform="translate(14 38) rotate(125) scale(.85)" fill="#a9d1b3" />
        <use href="#leaf" transform="translate(24 37) rotate(-135) scale(.85)" fill="#c2e3c8" />
        <use href="#leaf" transform="translate(88 32) rotate(-55) scale(.85)" fill="#93c2a1" />
        <use href="#leaf" transform="translate(98 32) rotate(55) scale(.85)" fill="#a9d1b3" />
        <use href="#leaf" transform="translate(128 34) rotate(40) scale(.8)" fill="#c2e3c8" />
        <use href="#leaf" transform="translate(144 19) rotate(-25) scale(.75)" fill="#93c2a1" />
        <use href="#leaf" transform="translate(152 36) rotate(-20) scale(.7)" fill="#a9d1b3" />
        <use href="#blossom" transform="translate(112 29) scale(.75)" fill="#f6cbd1" />
        <use href="#blossom" transform="translate(8 43) scale(.6)" fill="#e6dcf5" />
      </symbol>
    </defs>
  </svg>
</template>

<style scoped>
.sprite {
  position: absolute;
  width: 0;
  height: 0;
  overflow: hidden;
}
</style>
