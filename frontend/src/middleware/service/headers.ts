export function httpOptionsJson() {
    return {
        headers: {
            'Accept': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
        }
    }
}

export function httpOptionsUrlEnconded() {
    return {
        headers: {
            'Accept': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }
}