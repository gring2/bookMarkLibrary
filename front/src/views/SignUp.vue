<template>
  <section>
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
