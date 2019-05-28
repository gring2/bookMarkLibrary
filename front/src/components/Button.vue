<template>

    <a :class="className"><slot name="text"></slot></a>
</template>

<script lang="ts">
  import { Component, Prop, Vue } from 'vue-property-decorator';

  @Component
  export default class Button extends Vue {
    @Prop({default: ''}) private className!: string;
  }
</script>

<style scoped lang="css">
  a {
    color: black;
    width: 80px;
    height: 25px;
    background: #eee;
    padding: 10px;
    text-align: center;
    border-radius: 5px;
    font-weight: bold;
    text-decoration: none;
  }
</style>