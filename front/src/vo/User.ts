export default class User {
  public token!: string
  public email!: string
  private password?: string
  private password_confirm?: string
  constructor(email: string, password?: string, passwordConfirm?: string) {
    this.email = email
    this.password = password
    this.password_confirm = passwordConfirm
  }
}
