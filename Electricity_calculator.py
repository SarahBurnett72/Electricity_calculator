import streamlit as st

def calculate_cost(tarrif_blocks, spent_R, days, meter, buffer=3, per_day=10, tax=0.15):
    
    spent_kwh=calculate_kwh(spent_R, tarrif_blocks)
    
    kwh_needed=(days+buffer)*per_day-meter+spent_kwh
    
    remaining_kwh=kwh_needed
    total_cost=0
    
    for block in tarrif_blocks:
        if remaining_kwh<=0:
            break
        
        block_min=block["min_kwh"]
        block_max=block["max_kwh"]
        rate=block["rate"]
        
        if block_max is None:
            block_size=remaining_kwh
        else:
            block_size=block_max-block_min
        
        kwh_in_block=min(remaining_kwh, block_size)
        total_cost+=kwh_in_block*rate
        remaining_kwh-=kwh_in_block
        
    return total_cost*(1+tax) - spent_R, kwh_needed-spent_kwh 

def calculate_kwh(spent, tarrif_blocks, tax=0.15):
    net_amount=spent/(1+tax)
    
    remaining_money=net_amount
    total_kwh=0
    
    for block in tarrif_blocks:
        if remaining_money<=0:
            break
        
        block_min = block["min_kwh"]
        block_max = block["max_kwh"]
        rate = block["rate"]

        if block_max is None:
            # Unlimited block
            kwh_in_block = remaining_money / rate
            total_kwh += kwh_in_block
            break
        else:
            block_size = block_max - block_min

        full_block_cost = block_size * rate

        if remaining_money >= full_block_cost:
            total_kwh += block_size
            remaining_money -= full_block_cost
        else:
            kwh_in_block = remaining_money / rate
            total_kwh += kwh_in_block
            break

    return total_kwh

tarrif_blocks = [
    {"min_kwh": 0,   "max_kwh": 100,  "rate": 2.9790},
    {"min_kwh": 100,  "max_kwh": 400, "rate": 3.4864},
    {"min_kwh": 400, "max_kwh": 650, "rate": 3.7983},
    {"min_kwh": 650, "max_kwh": None, "rate": 4.0948}]
#%%
st.title("Prepaid electricity calculator")

st.write("Input the some information about the electricity you have bought this month, and calculate the optimal amount to buy!!")


st.divider()

def number_field(label, value=0, columns=None, **input_params):
    c1, c2 = st.columns([1, 1])

    # Display field name with some alignment
    #c1.markdown("##")
    c1.markdown(label)

    # Sets a default key parameter to avoid duplicate key errors
    input_params.setdefault("key", label)

    # Forward text input parameters
    return c2.number_input("", value=value, **input_params)

meter=number_field("Number on meter:")
spent_R=number_field("Amount spent on electricity this month:")
st.caption("This amount can be found in the little notebook on the microwave")
days=number_field("Number of days left in the month:")

col1, col2, col3 = st.columns([1,2,1])
with col2:
    clicked=st.button("Calculate")

if clicked:
    cost, kwh = calculate_cost(tarrif_blocks, spent_R, days, meter)
    
    st.divider()
    
    st.success(f"Buy: R{cost:.2f}")
    st.info(f"kWh purchased: {kwh:.2f}")
    
    st.header("Please enter this info in the book on the microwave")
    st.header("Meter number: 0428 790 666 5")

