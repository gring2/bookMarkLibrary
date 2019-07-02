<template>
  <input :type="type" @change="change" :placeholder='placeholder' :style="styles">
</template>

<script lang="ts">
  import { Component, Prop, Vue } from 'vue-property-decorator'

  @Component
  export default class Input extends Vue {
    @Prop({default: () => {
      return (): void => { return}
    }}) private change?: () => void
    @Prop() private placeholder?: string
    @Prop({default: () => Object.create({}) }) private styles!: object
    @Prop({default: 'text'}) private type!: string
  }
</script>

<style scoped lang="css">

</style>