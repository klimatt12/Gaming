resource "datadog_monitor" "process_alert_example" {
  name    = "Steam Gaming Session Ended"
  type    = "process alert"
  message = "Steam gaming session has ended. Exact details can be found [here](https://us5.datadoghq.com/dashboard/kz5-sr2-6hb/steam-game-summary?fromUser=false&refresh_mode=sliding&from_ts=1714177030188&to_ts=1714180630188&live=true) @myemail@gmail.com"
  query   = "processes('\"steamapps\\common\"').rollup('count').last('5m') < 1"
  monitor_thresholds {
    critical          = 1.0
    critical_recovery = 0.0
  }

  notify_no_data    = false
}