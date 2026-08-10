export interface UserCreate {
    username: string
    email: string
    password: string
}

export interface UserResponse {
    id: number
    username: string
    email: string
    is_active: boolean
}

export interface ForgotPasswordRequest {
    email: string
}

export interface ForgotPasswordResponse {
    message: string
    reset_token: string
}

export interface ResetPasswordRequest {
    token: string
    new_password: string
}
