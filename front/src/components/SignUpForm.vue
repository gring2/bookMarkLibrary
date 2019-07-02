<template>
  <div>
    <div>
      <label>Email: </label>
      <Input :change="(e) => { setData('email', e.target.value) }"/>
    </div>
    <div>
      <label>password: </label>
      <Input :type="'password'" :change="(e) => { setData('password', e.target.value) }" />
    </div>
    <div>
      <label>password confirm: </label>
      <Input :type="'password'" :change="(e) => { setData('passwordConFirm', e.target.value) }" />
    </div>
    <div>
      <Button :click="()=>{signup()}"><template v-slot:text >Susbmit</template></Button>
    </div>
  </div>
</template>

<script lang="ts">
  import { Component, Prop, Vue } from 'vue-property-decorator'
  import Input from '@/components/Input.vue'
  import Button from '@/components/Button.vue'
  import UserModule, {userMod} from '@/stores/modules/user'
  import User from '@/vo/User'

  @Component({
    components: {
      Input,
      Button
    }
  })
  export default class SignUpForm extends Vue {
    private password?: string
    private passwordConfirm?: string
    private email: string = ''

    private setData(key: string , data: string) {
      switch (key) {
        case 'password':
          this.password = data
          break
        case 'passwordConfirm':
          this.passwordConfirm = data
          break
        case 'email':
          this.email = data
          break
      }
    }

    private signup() {
      const user = new User(this.email, this.password, this.passwordConfirm)
      userMod.SIGN_UP(user)
    }
  }
</script>

<style lang="scss" scoped>
  label{
    display: block;
  }
  div {
    margin-bottom: 0.5rem;
    input {
      width: 20rem;
    }
  }
  div:last-of-type {
    margin-top: 1rem;
  }
</style>
