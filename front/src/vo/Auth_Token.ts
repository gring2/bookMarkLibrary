export default class Auth_Token {
  constructor(token: string | null) {
    this.token = token
  }

  public token: string | null

  public isvalid(): boolean {
    if(this.token && this.token.length > 0) return true
    return false
  }
}