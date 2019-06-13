export default class User {
  get email(): string {
    return this._email
  }

  set email(value: string) {
    this._email = value
  }
  private _email!: string
}