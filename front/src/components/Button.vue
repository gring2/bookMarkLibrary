<template>
    <button :class="className" v-bind:style="styles"><slot name="text"></slot></button>
</template>

<script lang="ts">
  import { Component, Prop, Vue } from 'vue-property-decorator'

  @Component
  export default class Button extends Vue {
    @Prop({default: ''}) private className!: string
    @Prop({default: () => Object.create({}) }) private styles!: object
  }
</script>

<style scoped lang="scss">
  button {
    color: black;
    width: 80px;
    height: 2rem;
    background: #eee;
    border: 0;
    text-align: center;
    border-radius: 5px;
    font-weight: bold;
    text-decoration: none;
    display: inline-block;
  }
</style>