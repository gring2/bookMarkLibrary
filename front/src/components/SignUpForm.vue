<template>
  <div>
    <div>
      <div>Email: </div>
      <Input :change="(e) => { setData('email', e.target.value) }"/>
    </div>
    <div>
      <div>password: </div>
      <Input :type="'password'" :change="(e) => { setData('password', e.target.value) }" />
    </div>
    <div>
      <div>password confirm: </div>
      <Input :type="'password'" :change="(e) => { setData('passwordConFirm', e.target.value) }" />
    </div>
  </div>
</template>

<script lang="ts">
  import { Component, Prop, Vue } from 'vue-property-decorator'
  import Input from '@/components/Input.vue'
  @Component({
    components: {
      Input
    }
  })
  export default class SignUpForm extends Vue {
    private password?: string
    private passwordConfirm?: string
    private email ?: string
    
    private setData(key:string , data: string) {
      switch (key) {
        case 'password':
          this.password = data
          break
        case 'passwordConfirm':
          this.passwordConfirm = data
          break;
        case 'email':
          this.email = data
          break;
      }
    }

  }
</script>

