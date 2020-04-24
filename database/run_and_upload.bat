FOR /L %%y IN (0, 1, 5000) DO python test_battle.py & TIMEOUT 1
cd game_telemetry
python read_data.py
cd ..