// tslint:disable-next-line:class-name
export default class Auth_Token {

  public token: string | null
  constructor(token: string | null) {
    this.token = token
  }

  public isvalid(): boolean {
    if (this.token && this.token.length > 0) { return true }
    return false
  }
}