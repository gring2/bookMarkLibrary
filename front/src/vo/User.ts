export default class User {
  constructor(email: string, password?: string, passwordConfirm?: string) {
    this.email = email
    this.password = password
    this.passwordConfirm = passwordConfirm
  }

  public token!: string
  public email!: string
  private password?: string
  private passwordConfirm?: string
}