import json
import uuid
import random
from datetime import datetime, timedelta

class ACPExtendedGenerator:
    def __init__(self):
        self.skus = ["sku_vintage_tee_gr_l", "sku_leather_boots_10", "sku_wireless_buds_v2", "sku_iphone_17_pro"]
        self.prices = [26.00, 120.00, 89.99, 1199.00]
        self.agents = ["agent_chatgpt_v5", "agent_claude_v4", "unknown_bot_net", "scraper_agent_x"]
        
    def _create_base_tx(self) -> dict:
        """Helper to create underlying valid transaction values."""
        item_idx = random.choices([0, 1, 2, 3], weights=[50, 30, 15, 5])[0]
        quantity = random.randint(1, 2) if item_idx != 3 else random.randint(1, 5)
        
        subtotal = round(self.prices[item_idx] * quantity, 2)
        shipping = 0.00 if subtotal >= 100.00 else 5.00
        tax = round(subtotal * 0.0825, 2)
        total = round(subtotal + shipping + tax, 2)
        
        return {
            "tx_id": f"tx_acp_{uuid.uuid4().hex[:12]}",
            "timestamp": (datetime.utcnow() - timedelta(minutes=random.randint(0, 1440))).strftime('%Y-%m-%dT%H:%M:%SZ'),
            "sku": self.skus[item_idx],
            "qty": quantity,
            "price": self.prices[item_idx],
            "subtotal": subtotal,
            "shipping": shipping,
            "tax": tax,
            "total": total
        }

    def generate_approved(self) -> dict:
        """Standard valid agentic commerce loop."""
        b = self._create_base_tx()
        return self._assemble_payload(b, "approved", "payment_settled", "spt_live_" + uuid.uuid4().hex[:15])

    def generate_declined(self) -> dict:
        """Simulates card issues or soft system failures."""
        b = self._create_base_tx()
        reason = random.choice(["insufficient_funds", "card_expired", "velocity_limit_exceeded"])
        return self._assemble_payload(b, f"declined_{reason}", "payment_failed", "spt_live_declined_" + uuid.uuid4().hex[:10])

    def generate_fraudulent(self) -> dict:
        """Simulates key ACP risk models: proxy distortion, mass orders, and broken signatures."""
        b = self._create_base_tx()
        fraud_type = random.choice(["velocity_attack", "token_hijack", "signature_spoof"])
        
        payload = self._assemble_payload(b, f"flagged_fraud_{fraud_type}", "gateway_rejected", "spt_hijacked_or_expired")
        
        # Inject structural/contextual anomalies based on the signature behavior of fraud
        # add noise by not following the usual transaction patterns in 20% of the below cases, skip this section
        if random.random() < 0.2:
            return payload  # Skip adding noise in 20% of the cases   
                
        if fraud_type == "velocity_attack":
            payload["initiation"]["agent"]["id"] = "unknown_bot_net"
            payload["initiation"]["cart"]["items"][0]["quantity"] = 50 # High volume item hoarding
            payload["proposal"]["totals"]["total"] = round(payload["proposal"]["totals"]["subtotal"] * 50, 2)
        elif fraud_type == "token_hijack":
            payload["settlement"]["payment_token"]["scoped_amount"] = 0.01 # Price tampering anomaly
        elif fraud_type == "signature_spoof":
            payload["settlement"]["buyer_verification"]["mandate_signature"] = "sig_INVALID_MALFORMED_DATA"
            
        return payload

    def _assemble_payload(self, b: dict, status: str, action_status: str, token: str) -> dict:
        return {
            "transaction_id": b["tx_id"],
            "timestamp": b["timestamp"],
            "outcome_metadata": {
                "simulation_label": status,
                "risk_score": random.randint(0, 15) if "approved" in status else random.randint(75, 100)
            },
            "initiation": {
                "acp_version": "2026-04-17",
                "agent": {"id": random.choice(self.agents[:2]), "provider": "AI_Corp"},
                "cart": {"items": [{"sku": b["sku"], "quantity": b["qty"], "unit_price": b["price"], "currency": "USD"}]},
                "shipping_address": {"postal_code": str(random.randint(10000, 99999)), "country": "US"}
            },
            "proposal": {
                "status": "proposal_created" if "fraud" not in status else "security_flagged",
                "totals": {"subtotal": b["subtotal"], "shipping": b["shipping"], "tax": b["tax"], "total": b["total"], "currency": "USD"}
            },
            "settlement": {
                "action": action_status,
                "payment_token": {"token_id": token, "network_provider": "stripe_acp_v1", "scoped_amount": b["total"], "currency": "USD"},
                "buyer_verification": {"protocol": "AP2", "mandate_signature": f"sig_ed25519_{uuid.uuid4().hex[:10]}"}
            }
        }

    def build(self, filename: str, count: int):
        print(f"Compiling {count} mixed-state ACP records...")
        with open(filename, 'w') as f:
            f.write("[\n")
            for i in range(count):
                # Probabilistic routing
                roll = random.random()
                if roll < 0.85:
                    record = self.generate_approved()
                elif roll < 0.95:
                    record = self.generate_declined()
                else:
                    record = self.generate_fraudulent()
                    
                f.write(json.dumps(record, indent=2))
                if i < count - 1:
                    f.write(",\n")
            f.write("\n]")
        print(f"Done. Saved to {filename}")

if __name__ == "__main__":
    ACPExtendedGenerator().build("acp_mixed_outcomes_w_noise.json", 50000)
