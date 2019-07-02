<template>
  <section class="content">
    <SignInForm/>
  </section>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import SignInForm from '@/components/SignInForm.vue'
@Component({
  components: {
    SignInForm
  },
})
export default class SignIn extends Vue {}
</script>

<style lang="scss" scoped>
  section {
    display: flex;
    justify-content: center;
    align-items: center
  }
</style>

