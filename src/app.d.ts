
declare global {
	namespace App {
        interface Locals {
            user?: {
                id: string;
                email: string;
            };
            session: import("$lib/server/auth").SessionValidationResult["session"];
        }
    }
}

export {};
