<template>
  <section class="content">
    <SignUpForm/>
  </section>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import SignUpForm from '@/components/SignUpForm.vue'
@Component({
  components: {
    SignUpForm
  },
})
export default class SignUp extends Vue {}
</script>

<style lang="scss" scoped>
  section {
    display: flex;
    justify-content: center;
    align-items: center
  }
</style>

