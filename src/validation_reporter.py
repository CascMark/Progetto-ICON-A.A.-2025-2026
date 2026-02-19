import os
import json

class ValidationReporter:
    def __init__(self, model_dir):
        self.metrics_path = os.path.join(model_dir, "metrics.json")

    def get_formatted_report(self, risultati_ml=None):
        report = []
        if not os.path.exists(self.metrics_path):
            return "⚠️ Metriche non trovate."

        try:
            with open(self.metrics_path, 'r') as f:
                metrics = json.load(f)
        except Exception as e:
            return f"❌ Errore lettura metriche: {e}"

        report.append(f"{'Algoritmo':<18} | {'Accuratezza':<11} | {'Varianza':<9} | {'Deviaz.':<8} | {'F1-score':<8} | {'AVG(P)':<8} | {'AUC':<8}")
        report.append("-" * 88)
        
        try:
            for name, m in metrics.items():
                acc = m.get('Accuratezza', 0.0)
                var = m.get('Varianza', 0.0)
                dev = m.get('Deviazione', 0.0)
                f1  = m.get('F1-score', 0.0)
                avg_p = m.get('AVG(P)', 0.0)
                auc = m.get('AUC', -1.0)
                
                acc_str = f"{acc:.3f}"
                var_str = f"{var:.5f}" if var > 0 else "0.00000" # Aumentati i decimali per mostrare il valore reale
                dev_str = f"{dev:.3f}"
                f1_str  = f"{f1:.3f}" if f1 > 0 else "//"
                avg_p_str = f"{avg_p:.3f}" if avg_p > 0 else "//"
                auc_str = f"{auc:.3f}" if auc >= 0 else "//"
                
                report.append(f"{name:<18} | {acc_str:<11} | {var_str:<9} | {dev_str:<8} | {f1_str:<8} | {avg_p_str:<8} | {auc_str:<8}")
        except Exception as e:
             return f"❌ Errore format. Esegui train_model.py. Dettaglio: {e}"
        
        report.append("-" * 88)
        report.append("[*] Nota: Valori calcolati tramite 10-Fold Cross-Validation Stratificata.")

        if risultati_ml:
            report.append("\n" + "="*88)
            report.append("   CHECK CONSENSO (MULTI-MODEL VOTE)")
            report.append("="*88)
            rf_pred = risultati_ml.get("RF", "N/A")
            nn_pred = risultati_ml.get("NN", "N/A")
            if rf_pred == nn_pred:
                report.append(f"-> ESITO: CONSENSO UNANIME")
                report.append(f"   I modelli convergono sulla diagnosi: {rf_pred}")
            else:
                report.append("-> ESITO: DISCORDANZA RILEVATA")
                report.append(f"   Random Forest indica: {rf_pred} | Rete Neurale indica: {nn_pred}")
        
        return "\n".join(report)