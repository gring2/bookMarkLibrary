export default class User {
  get email(): string {
    return this._email
  }

  set email(value: string) {
    this._email = value
  }

  public token!: string
  private _email!: string
}