# Linear interpolation attempt
send_arr = df['send_rates'].to_numpy()
send_arr = np.insert(send_arr, range(1, len(send_arr)), 0)
send_df = pd.DataFrame(send_arr)\
    .replace(0, np.nan)\
    .interpolate(method='linear', limit_direction='forward')
receive_arr = df['receive_rates'].to_numpy()
receive_arr = np.insert(receive_arr, range(1, len(receive_arr)), 0)
receive_df = pd.DataFrame(receive_arr)\
    .replace(0, np.nan)\
    .interpolate(method='linear', limit_direction='forward')
network_data = {
    'send_rates': [send_df],
    'receive_rate': [receive_df]
}
df = pd.DataFrame(network_data)